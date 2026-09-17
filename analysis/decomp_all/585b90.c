
void FUN_00585b90(undefined4 *param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  
  if ((param_1 == (undefined4 *)0x0) &&
     (iVar2 = FUN_00573780(2,"_getbuf.c",0x2e,0,"str != NULL"), iVar2 == 1)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  DAT_0080a4e0 = DAT_0080a4e0 + 1;
  uVar3 = __malloc_dbg(0x1000,2,"_getbuf.c",0x3b);
  param_1[2] = uVar3;
  if (param_1[2] == 0) {
    param_1[3] = param_1[3] | 4;
    param_1[2] = param_1 + 5;
    param_1[6] = 2;
  }
  else {
    param_1[3] = param_1[3] | 8;
    param_1[6] = 0x1000;
  }
  *param_1 = param_1[2];
  param_1[1] = 0;
  return;
}

