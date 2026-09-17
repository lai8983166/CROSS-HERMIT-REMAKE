
void FUN__text__004ddc60(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((param_2 == -1) &&
     (iVar2 = FUN__text__00424f80("skill != -1","E:\\CrossHermit\\GAME\\SRC\\Common\\ComYken.cpp",
                                  DAT_00738c94 + 5,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_10 = &DAT_006c2dc8 + param_2 * 0x48;
  local_c = &DAT_006b2d88 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40;
  if ((&DAT_006c2de0)[param_2 * 0x48] == '\x06') {
    if (param_2 < 0x65) {
      FUN__text__004ddd50(param_1,param_2);
    }
  }
  else if (param_2 < 0x65) {
    FUN__text__004ddf40(param_1,param_2);
  }
  local_8 = 0x4ddd3f;
  FUN__text__0056ce80();
  return;
}

