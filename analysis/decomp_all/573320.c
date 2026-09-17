
undefined4 FUN__text__00573320(char *param_1,char *param_2)

{
  char cVar1;
  undefined4 uVar2;
  size_t _Count;
  int local_8;
  
  _memset(param_1,0,0x88);
  if (*param_2 == '\0') {
    uVar2 = 0;
  }
  else if ((*param_2 == '.') && (param_2[1] != '\0')) {
    FUN__text__0056cd90(param_1 + 0x80,param_2 + 1);
    uVar2 = 0;
  }
  else {
    local_8 = 0;
    while (_Count = FUN__text__00581f10(param_2,&DAT_005f9dc4), _Count != 0) {
      cVar1 = param_2[_Count];
      if (((local_8 == 0) && ((int)_Count < 0x40)) && (cVar1 != '.')) {
        _strncpy(param_1,param_2,_Count);
      }
      else if (((local_8 == 1) && ((int)_Count < 0x40)) && (cVar1 != '_')) {
        _strncpy(param_1 + 0x40,param_2,_Count);
      }
      else {
        if ((local_8 != 2) || ((cVar1 != '\0' && (cVar1 != ',')))) {
          return 0xffffffff;
        }
        _strncpy(param_1 + 0x80,param_2,_Count);
      }
      if ((cVar1 == ',') || (cVar1 == '\0')) {
        return 0;
      }
      param_2 = param_2 + _Count + 1;
      local_8 = local_8 + 1;
    }
    uVar2 = 0xffffffff;
  }
  return uVar2;
}

