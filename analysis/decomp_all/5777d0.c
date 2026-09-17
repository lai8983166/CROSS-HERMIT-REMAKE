
undefined4 FUN__text__005777d0(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  int local_c;
  
  if ((param_1 == (undefined4 *)0x0) &&
     (iVar2 = FUN__text__00573780(2,"_sftbuf.c",0x41,0,"str != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    uVar3 = (*pcVar1)();
    return uVar3;
  }
  iVar2 = __isatty(param_1[4]);
  if (iVar2 == 0) {
    return 0;
  }
  if (param_1 == (undefined4 *)&DAT_00761ed0) {
    local_c = 0;
  }
  else {
    if (param_1 != (undefined4 *)&DAT_00761ef0) {
      return 0;
    }
    local_c = 1;
  }
  DAT_0080a4e0 = DAT_0080a4e0 + 1;
  if ((param_1[3] & 0x10c) != 0) {
    return 0;
  }
  if (*(int *)(&DAT_0080a4e4 + local_c * 4) == 0) {
    uVar3 = __malloc_dbg(0x1000,2,"_sftbuf.c",0x5e);
    *(undefined4 *)(&DAT_0080a4e4 + local_c * 4) = uVar3;
    if (*(int *)(&DAT_0080a4e4 + local_c * 4) == 0) {
      param_1[2] = param_1 + 5;
      *param_1 = param_1[2];
      param_1[6] = 2;
      param_1[1] = 2;
      goto LAB__text__00577909;
    }
  }
  param_1[2] = *(undefined4 *)(&DAT_0080a4e4 + local_c * 4);
  *param_1 = param_1[2];
  param_1[6] = 0x1000;
  param_1[1] = 0x1000;
LAB__text__00577909:
  param_1[3] = param_1[3] | 0x1102;
  return 1;
}

