
int FUN__text__00470720(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_1 % 0x5a < 0x1e) {
    local_c = (int)(char)(&DAT_006187dc)[param_1 / 0xb];
  }
  else if (param_1 % 0x5a < 0x3d) {
    local_c = (int)(char)(&DAT_006187b8)[param_1 / 0xb];
  }
  else {
    local_c = (int)(char)(&DAT_006187dc)[param_1 / 0xb];
  }
  return local_c;
}

