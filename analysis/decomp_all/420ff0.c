
void FUN__text__00420ff0(int param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  uint local_14;
  uint local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = *(ushort *)(param_2 + 2) & 7;
  if (local_10 == 1) {
    local_14 = (uint)*(ushort *)(param_1 + 0x1c);
    if (local_14 == 8) {
      local_c = FUN__text__004210d0(param_1,param_2,param_3,param_4);
    }
    else {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\Format.cpp",
                                  DAT_005ff5ec + 7,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_c = 1;
    }
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\Format.cpp",
                                DAT_005ff5ec + 0xd,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x4210c8;
  FUN__text__0056ce80();
  return;
}

