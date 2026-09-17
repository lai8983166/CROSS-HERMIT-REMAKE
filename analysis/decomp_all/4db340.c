
void FUN__text__004db340(int param_1,void *param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  _memset(param_2,0,0x4c);
  for (local_c = 0; local_c != 8; local_c = local_c + 1) {
    local_8 = (int)*(short *)(param_1 + 0x52 + local_c * 2);
    if ((local_8 != 0) && (local_8 != 0xffff)) {
      FUN__text__004dcf00(local_8,param_1,param_2,0);
    }
  }
  for (local_c = 0; local_c != 8; local_c = local_c + 1) {
    local_8 = (int)*(short *)(param_1 + 0x62 + local_c * 2);
    if ((local_8 != 0) && (local_8 != 0xffff)) {
      FUN__text__004dd510(local_8,param_1,(int)param_2 + 0x24,0);
    }
  }
  local_8 = 0x4db412;
  FUN__text__0056ce80();
  return;
}

