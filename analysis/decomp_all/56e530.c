
undefined4 FUN__text__0056e530(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  if ((param_1 == 0) && (iVar2 = FUN__text__00573780(2,"fclose.c",0x77,0,"str != NULL"), iVar2 == 1)
     ) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  if ((*(uint *)(param_1 + 0xc) & 0x83) != 0) {
    local_8 = FUN__text__005775c0(param_1);
    FUN__text__00577480(param_1);
    iVar2 = FUN__text__00577350(*(undefined4 *)(param_1 + 0x10));
    if (iVar2 < 0) {
      local_8 = 0xffffffff;
    }
    else if (*(int *)(param_1 + 0x1c) != 0) {
      __free_dbg(*(undefined4 *)(param_1 + 0x1c),2);
      *(undefined4 *)(param_1 + 0x1c) = 0;
    }
  }
  *(undefined4 *)(param_1 + 0xc) = 0;
  return local_8;
}

