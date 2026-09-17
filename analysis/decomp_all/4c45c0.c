
void FUN__text__004c45c0(undefined4 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 local_120 [16];
  undefined *local_e0;
  undefined1 local_dc [200];
  uint local_14;
  ushort local_10;
  undefined2 uStack_e;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_120;
  for (iVar2 = 0x47; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__004128f0(0x39,0);
  if (iVar2 == 0) {
    local_c = param_2;
    _local_10 = CONCAT22(uStack_e,*(ushort *)(param_2 + 4));
    local_14 = CONCAT22(local_14._2_2_,*(undefined2 *)(param_2 + 6));
    local_e0 = (&PTR_PTR_00621988)[*(ushort *)(param_2 + 4)];
    FUN__text__004cd7b0("data\\sound\\voice\\",local_dc);
    FUN__text__004cd810(local_dc,*(undefined4 *)(local_e0 + (local_14 & 0xffff) * 4));
    if (DAT_007a49fc != 0) {
      FUN__text__0041e500();
      uVar4 = 0;
      uVar1 = FUN__text__004501d0(local_dc);
      FUN__text__0041e190(uVar1,uVar4);
      FUN__text__0042b2d0("[ ADV VIOCE ] : %s \n",local_dc);
    }
  }
  local_8 = 0x4c46e8;
  FUN__text__0056ce80();
  return;
}

