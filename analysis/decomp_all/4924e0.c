
void FUN__text__004924e0(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(char *)(param_2 + 0x34) != '\0') {
    local_c = FUN__text__00467e00("E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                  DAT_00619250 + 7);
    local_c = local_c % 100;
    if (local_c < 100) {
      FUN__text__004902e0(param_2,param_2 + 0x34,2);
    }
  }
  local_8 = 0x492556;
  FUN__text__0056ce80();
  return;
}

