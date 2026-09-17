
void __fastcall FUN__text__0044dd90(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0xb0) = 0;
  *(undefined1 *)(param_1 + 0xbb) = 0xff;
  *(undefined1 *)(param_1 + 0xb8) = 0x80;
  *(undefined1 *)(param_1 + 0xb9) = 0x80;
  *(undefined1 *)(param_1 + 0xba) = 0x80;
  local_c = 0x138;
  local_10 = 299;
  local_8 = param_1;
  FUN__text__0044e140(param_1 + 0x54,0x138,299,0x5f,1,&DAT_006068a8);
  if (*(int *)(local_8 + 0x38) != -1) {
    FUN__text__0044e140(local_8 + 0x54,(int)local_c + (int)DAT_006067b0,
                        (int)local_10 + (int)DAT_006067b2,0x50,1,&DAT_006068b0);
  }
  local_14 = local_c + *(short *)(&DAT_006067b8 + *(int *)(local_8 + 0x48) * 8);
  local_18 = local_10 + *(short *)(&DAT_006067ba + *(int *)(local_8 + 0x48) * 8);
  FUN__text__0044df40((int)local_14,(int)local_18,*(undefined4 *)(local_8 + 0x48));
  local_14 = local_c + *(short *)(&DAT_00606808 + *(int *)(local_8 + 0x4c) * 8);
  local_18 = local_10 + *(short *)(&DAT_0060680a + *(int *)(local_8 + 0x4c) * 8);
  FUN__text__0044df40((int)local_14,(int)local_18,*(undefined4 *)(local_8 + 0x4c));
  local_14 = local_c + *(short *)(&DAT_00606858 + *(int *)(local_8 + 0x50) * 8);
  local_18 = local_10 + *(short *)(&DAT_0060685a + *(int *)(local_8 + 0x50) * 8);
  FUN__text__0044df40((int)local_14,(int)local_18,*(undefined4 *)(local_8 + 0x50));
  local_8 = 0x44df35;
  FUN__text__0056ce80();
  return;
}

