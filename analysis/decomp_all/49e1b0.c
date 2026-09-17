
/* WARNING: Removing unreachable block (ram,0x0049e1ce) */
/* WARNING: Removing unreachable block (ram,0x0049e1f1) */

void FUN__text__0049e1b0(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined **ppuVar5;
  undefined4 local_4c [16];
  undefined4 *local_c;
  undefined4 *local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__004e1a10();
  FUN__text__004e1b60();
  FUN__text__004e2d00(&DAT_00809320);
  FUN__text__00415d90();
  local_8 = (undefined4 *)FUN__text__004e2f50();
  if (local_8 != (undefined4 *)0x0) {
    puVar3 = local_8;
    puVar4 = &DAT_00809320;
    for (iVar2 = 10; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
    FUN__text__004e2d00(&DAT_00809320);
    local_c = local_8;
    FUN__text__00428ad0(local_8);
  }
  ppuVar5 = &PTR_s_data_sound_plw_Common_E_SE04_WAV_0061b010;
  uVar1 = FUN__text__00450110(&DAT_005953ac);
  FUN__text__0040c780(0,uVar1,ppuVar5);
  FUN__text__00439e30(0);
  FUN__text__00415480(1,10);
  local_8 = (undefined4 *)0x49e2a7;
  FUN__text__0056ce80();
  return;
}

