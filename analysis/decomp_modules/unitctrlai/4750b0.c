
void FUN__text__004750b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x290;
  iVar1 = FUN__text__00468d80(param_1);
  if (iVar1 == 0) {
    local_10 = (&PTR_DAT_006a7f6c)[DAT_007f4488] + (0xf9 - *(short *)(param_1 + 2)) * 0x54;
    FUN__text__004da710(local_10,param_1);
  }
  local_8 = 0x475131;
  FUN__text__0056ce80();
  return;
}

