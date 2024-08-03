from .example_mod import do_primes
from .version import version as __version__

# Then you can be explicit to control what ends up in the namespace,
__all__ = ['do_primes']
