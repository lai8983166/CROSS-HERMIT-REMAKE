
void FUN__text__0044cba0(int param_1,undefined4 param_2,short param_3,short param_4,
                        undefined2 param_5,undefined4 param_6,short *param_7)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__004077c0(DAT_007a49fc);
  FUN__text__00407870(param_2,param_6);
  *(undefined2 *)(param_1 + 0x58) = 0xc0;
  *(undefined2 *)(param_1 + 0x76) = param_5;
  *(short *)(param_1 + 0x38) = param_7[2];
  *(short *)(param_1 + 0x3a) = param_7[3];
  *(short *)(param_1 + 0x78) = *param_7;
  *(short *)(param_1 + 0x7a) = param_7[1];
  *(short *)(param_1 + 0x7c) = *param_7 + *(short *)(param_1 + 0x38);
  *(short *)(param_1 + 0x7e) = param_7[1] + *(short *)(param_1 + 0x3a);
  FUN__text__004079c0((int)param_3,(int)param_4);
  local_8 = 0x44cc72;
  FUN__text__0056ce80();
  return;
}

