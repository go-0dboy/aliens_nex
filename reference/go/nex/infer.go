package nex

import "fmt"

type inferState struct {
	fresh *FreshTypeVars
}

// InferClosed validates a NEX-1 Core term and returns its principal type scheme.
// It performs no evaluation. Scope and Core primitive validity are checked before
// type inference so static error classes remain distinct.
func InferClosed(term *Term) (TypeScheme, error) {
	if err := ValidateClosed(term); err != nil {
		return TypeScheme{}, err
	}
	if err := ValidateCorePrimitives(term); err != nil {
		return TypeScheme{}, err
	}

	state := &inferState{fresh: NewFreshTypeVars(0)}
	sub, typ, err := state.infer(nil, term)
	if err != nil {
		return TypeScheme{}, err
	}
	finalType, err := ApplyType(sub, typ)
	if err != nil {
		return TypeScheme{}, err
	}
	return Generalize(nil, finalType)
}

func (s *inferState) infer(env TypeEnv, term *Term) (Substitution, *Type, error) {
	switch term.Kind {
	case KindVar:
		index, ok := envIndex(term, len(env))
		if !ok {
			return nil, nil, &ScopeError{Index: cloneNat(term.Value), Depth: len(env)}
		}
		typ, err := Instantiate(env[index], s.fresh)
		if err != nil {
			return nil, nil, err
		}
		return EmptySubstitution(), typ, nil

	case KindLam:
		parameter := s.fresh.Fresh()
		bodyEnv := prependScheme(MonoScheme(parameter), env)
		sub, bodyType, err := s.infer(bodyEnv, term.A)
		if err != nil {
			return nil, nil, err
		}
		parameterType, err := ApplyType(sub, parameter)
		if err != nil {
			return nil, nil, err
		}
		bodyType, err = ApplyType(sub, bodyType)
		if err != nil {
			return nil, nil, err
		}
		return sub, TFunc(parameterType, bodyType), nil

	case KindApp:
		s1, functionType, err := s.infer(env, term.A)
		if err != nil {
			return nil, nil, err
		}
		env1, err := ApplyEnv(s1, env)
		if err != nil {
			return nil, nil, err
		}
		s2, argumentType, err := s.infer(env1, term.B)
		if err != nil {
			return nil, nil, err
		}

		functionType, err = ApplyType(s2, functionType)
		if err != nil {
			return nil, nil, err
		}
		argumentType, err = ApplyType(s2, argumentType)
		if err != nil {
			return nil, nil, err
		}
		resultType := s.fresh.Fresh()
		s3, err := Unify(functionType, TFunc(argumentType, resultType))
		if err != nil {
			return nil, nil, err
		}

		s21, err := ComposeSubstitutions(s2, s1)
		if err != nil {
			return nil, nil, err
		}
		total, err := ComposeSubstitutions(s3, s21)
		if err != nil {
			return nil, nil, err
		}
		resultType, err = ApplyType(s3, resultType)
		if err != nil {
			return nil, nil, err
		}
		return total, resultType, nil

	case KindLet:
		s1, valueType, err := s.infer(env, term.A)
		if err != nil {
			return nil, nil, err
		}
		env1, err := ApplyEnv(s1, env)
		if err != nil {
			return nil, nil, err
		}
		valueType, err = ApplyType(s1, valueType)
		if err != nil {
			return nil, nil, err
		}
		scheme, err := Generalize(env1, valueType)
		if err != nil {
			return nil, nil, err
		}
		bodyEnv := prependScheme(scheme, env1)
		s2, bodyType, err := s.infer(bodyEnv, term.B)
		if err != nil {
			return nil, nil, err
		}
		total, err := ComposeSubstitutions(s2, s1)
		if err != nil {
			return nil, nil, err
		}
		bodyType, err = ApplyType(s2, bodyType)
		if err != nil {
			return nil, nil, err
		}
		return total, bodyType, nil

	case KindNat:
		return EmptySubstitution(), TNat(), nil

	case KindPrim:
		primitive, err := LookupCorePrimitive(term.Value)
		if err != nil {
			return nil, nil, err
		}
		typ, err := Instantiate(primitive.Scheme, s.fresh)
		if err != nil {
			return nil, nil, err
		}
		return EmptySubstitution(), typ, nil

	default:
		return nil, nil, fmt.Errorf("%w: unsupported term kind %d", ErrInvalidTerm, term.Kind)
	}
}

func prependScheme(scheme TypeScheme, env TypeEnv) TypeEnv {
	out := make(TypeEnv, 0, len(env)+1)
	out = append(out, scheme)
	out = append(out, env...)
	return out
}

func envIndex(term *Term, envLen int) (int, bool) {
	if term == nil || term.Value == nil || term.Value.Sign() < 0 || !term.Value.IsUint64() {
		return 0, false
	}
	index := term.Value.Uint64()
	if index >= uint64(envLen) {
		return 0, false
	}
	return int(index), true
}
