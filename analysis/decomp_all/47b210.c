
void FUN__text__0047b210(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((*(short *)(param_1 + 0x4ee) != -1) &&
     (*(short *)(param_1 + 0x4ee) != *(short *)(param_2 + 2))) {
    local_10 = FUN__text__0047a8e0(param_1);
    local_c = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e3c + 0xb);
    local_c = local_c % 100;
  }
  local_8 = 0x47b2b0;
  FUN__text__0056ce80();
  return;
}

