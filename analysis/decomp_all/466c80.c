
void FUN__text__00466c80(char *param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  uint local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*param_1 == '\0') {
    iVar2 = FUN__text__00424f80("tbl->Used!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618b30 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined2 *)(param_1 + 2) = (undefined2)param_2;
  param_1[1] = (char)param_3;
  local_c = *(int *)(param_1 + 4);
  local_10 = FUN__text__00464d70(DAT_007a49fc,param_2 + 8);
  *(undefined4 *)(local_c + 0x28) = *(undefined4 *)(local_8 + 0x2e6f0);
  *(int *)(local_8 + 0x2e6f0) = *(int *)(local_8 + 0x2e6f0) + 1;
  local_14 = (uint)(param_3 != 0);
  local_10 = FUN__text__00464eb0((&PTR_s_data_DxAnim_b1a_bin_00610538)[param_2 * 2],param_3,local_14
                                 ,0);
  if (local_10 != 0) {
    iVar2 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618b30 + 0x10,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  FUN__text__0040b960(1);
  local_8 = 0x466d94;
  FUN__text__0056ce80();
  return;
}

