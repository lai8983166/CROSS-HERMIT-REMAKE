
void __thiscall FUN__text__0043b9e0(int param_1,int param_2,int param_3,int param_4,int param_5)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((((param_2 < 0) || (param_3 < 0)) || (*(short *)(*(int *)(param_1 + 0x2659c) + 4) <= param_2))
     || (*(short *)(*(int *)(param_1 + 0x2659c) + 6) <= param_3)) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                DAT_005ff9e4 + 0x16,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    *(undefined4 *)(param_5 + 0x10) = 0;
    *(undefined4 *)(param_5 + 0x14) = 0;
    *(undefined4 *)(param_5 + 0x18) = 0;
  }
  else {
    local_c = param_3 * *(short *)(*(int *)(param_1 + 0x2659c) + 4) + param_2;
    local_10 = CONCAT31(local_10._1_3_,
                        *(undefined1 *)(*(int *)(param_1 + 0x2659c) + 0x10 + local_c * 6));
    if (((param_4 < 0) || (4 < param_4)) &&
       (iVar2 = FUN__text__00424f80("(0<=type)&&(type<=4)",
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                    DAT_005ff9e4 + 0xd,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (param_4 == 4) {
      param_4 = 0;
    }
    *(undefined4 *)(param_5 + 0x10) =
         *(undefined4 *)
          (*(int *)(local_8 + 0x8c) + (local_10 & 0xff) * 0x4c + 0x10 + param_4 * 0x10);
    *(undefined4 *)(param_5 + 0x14) =
         *(undefined4 *)
          (*(int *)(local_8 + 0x8c) + (local_10 & 0xff) * 0x4c + 0x14 + param_4 * 0x10);
    *(undefined4 *)(param_5 + 0x18) =
         *(undefined4 *)
          (*(int *)(local_8 + 0x8c) + (local_10 & 0xff) * 0x4c + 0x18 + param_4 * 0x10);
  }
  local_8 = 0x43bb83;
  FUN__text__0056ce80();
  return;
}

