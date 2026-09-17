
/* Library Function - Single Match
    _GetPrimaryLen
   
   Libraries: Visual Studio 2003 Debug, Visual Studio 2005 Debug, Visual Studio 2008 Debug, Visual
   Studio 2010 Debug */

int _GetPrimaryLen(char *param_1)

{
  int local_c;
  char local_8;
  
  local_c = 0;
  local_8 = *param_1;
  while (((param_1 = param_1 + 1, '@' < local_8 && (local_8 < '[')) ||
         (('`' < local_8 && (local_8 < '{'))))) {
    local_c = local_c + 1;
    local_8 = *param_1;
  }
  return local_c;
}

