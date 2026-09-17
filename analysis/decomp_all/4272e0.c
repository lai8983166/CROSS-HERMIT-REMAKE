
void __thiscall FUN__text__004272e0(int param_1,undefined4 param_2,int param_3,int param_4)

{
  size_t sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_74 [20];
  size_t local_24;
  uint local_20;
  undefined4 local_1c;
  size_t local_18;
  int local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_3 == 0x102) {
    local_8 = param_1;
    local_18 = _strlen((char *)(param_1 + 0x63c));
    if ((param_4 == 8) && (0 < (int)local_18)) {
      *(undefined1 *)(local_8 + local_18 + 0x63b) = 0;
    }
    if ((int)(local_18 + 1) < *(int *)(local_8 + 0x638)) {
      local_1c = 0;
      local_20 = 0;
      while( true ) {
        sVar1 = _strlen(
                       " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*,.=`~!@#$%^&*()_|/"
                       );
        if (sVar1 <= local_20) break;
        if (param_4 ==
            " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-*,.=`~!@#$%^&*()_|/"
            [local_20]) {
          local_24 = _strlen((char *)(local_8 + 0x63c));
          *(undefined1 *)(local_8 + local_24 + 0x63c) = (undefined1)param_4;
          *(undefined1 *)(local_8 + local_24 + 0x63d) = 0;
          local_1c = 1;
        }
        local_20 = local_20 + 1;
      }
    }
  }
  local_8 = 0x427521;
  FUN__text__0056ce80();
  return;
}

