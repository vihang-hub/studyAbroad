"""
Supabase client for backend (Python)
Service role access for server-side operations
"""

from typing import Optional
from supabase import create_client, Client
from src.config import settings

# Global Supabase client with service role key (full access)
_supabase_client: Optional[Client] = None
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg is not None:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


def x_get_supabase__mutmut_orig() -> Client:
    """
    Get Supabase client instance with service role key
    This client has full access and bypasses RLS policies
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

    return _supabase_client


def x_get_supabase__mutmut_1() -> Client:
    """
    Get Supabase client instance with service role key
    This client has full access and bypasses RLS policies
    """
    global _supabase_client

    if _supabase_client is not None:
        _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

    return _supabase_client


def x_get_supabase__mutmut_2() -> Client:
    """
    Get Supabase client instance with service role key
    This client has full access and bypasses RLS policies
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = None

    return _supabase_client


def x_get_supabase__mutmut_3() -> Client:
    """
    Get Supabase client instance with service role key
    This client has full access and bypasses RLS policies
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = create_client(None, settings.SUPABASE_SERVICE_ROLE_KEY)

    return _supabase_client


def x_get_supabase__mutmut_4() -> Client:
    """
    Get Supabase client instance with service role key
    This client has full access and bypasses RLS policies
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = create_client(settings.SUPABASE_URL, None)

    return _supabase_client


def x_get_supabase__mutmut_5() -> Client:
    """
    Get Supabase client instance with service role key
    This client has full access and bypasses RLS policies
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = create_client(settings.SUPABASE_SERVICE_ROLE_KEY)

    return _supabase_client


def x_get_supabase__mutmut_6() -> Client:
    """
    Get Supabase client instance with service role key
    This client has full access and bypasses RLS policies
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = create_client(settings.SUPABASE_URL, )

    return _supabase_client

x_get_supabase__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_supabase__mutmut_1': x_get_supabase__mutmut_1, 
    'x_get_supabase__mutmut_2': x_get_supabase__mutmut_2, 
    'x_get_supabase__mutmut_3': x_get_supabase__mutmut_3, 
    'x_get_supabase__mutmut_4': x_get_supabase__mutmut_4, 
    'x_get_supabase__mutmut_5': x_get_supabase__mutmut_5, 
    'x_get_supabase__mutmut_6': x_get_supabase__mutmut_6
}

def get_supabase(*args, **kwargs):
    result = _mutmut_trampoline(x_get_supabase__mutmut_orig, x_get_supabase__mutmut_mutants, args, kwargs)
    return result 

get_supabase.__signature__ = _mutmut_signature(x_get_supabase__mutmut_orig)
x_get_supabase__mutmut_orig.__name__ = 'x_get_supabase'


def x_get_supabase_anon__mutmut_orig() -> Client:
    """
    Get Supabase client with anon key (respects RLS policies)
    Use this when you want to enforce Row Level Security
    """
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)


def x_get_supabase_anon__mutmut_1() -> Client:
    """
    Get Supabase client with anon key (respects RLS policies)
    Use this when you want to enforce Row Level Security
    """
    return create_client(None, settings.SUPABASE_ANON_KEY)


def x_get_supabase_anon__mutmut_2() -> Client:
    """
    Get Supabase client with anon key (respects RLS policies)
    Use this when you want to enforce Row Level Security
    """
    return create_client(settings.SUPABASE_URL, None)


def x_get_supabase_anon__mutmut_3() -> Client:
    """
    Get Supabase client with anon key (respects RLS policies)
    Use this when you want to enforce Row Level Security
    """
    return create_client(settings.SUPABASE_ANON_KEY)


def x_get_supabase_anon__mutmut_4() -> Client:
    """
    Get Supabase client with anon key (respects RLS policies)
    Use this when you want to enforce Row Level Security
    """
    return create_client(settings.SUPABASE_URL, )

x_get_supabase_anon__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_supabase_anon__mutmut_1': x_get_supabase_anon__mutmut_1, 
    'x_get_supabase_anon__mutmut_2': x_get_supabase_anon__mutmut_2, 
    'x_get_supabase_anon__mutmut_3': x_get_supabase_anon__mutmut_3, 
    'x_get_supabase_anon__mutmut_4': x_get_supabase_anon__mutmut_4
}

def get_supabase_anon(*args, **kwargs):
    result = _mutmut_trampoline(x_get_supabase_anon__mutmut_orig, x_get_supabase_anon__mutmut_mutants, args, kwargs)
    return result 

get_supabase_anon.__signature__ = _mutmut_signature(x_get_supabase_anon__mutmut_orig)
x_get_supabase_anon__mutmut_orig.__name__ = 'x_get_supabase_anon'
