
void FUN__text__00429990(char *param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  char *local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  iVar1 = FUN__text__00429820(*param_1);
  if (iVar1 == 0) {
    for (local_c = 0; *(char *)(param_3 + local_c) != '\0'; local_c = local_c + 1) {
      if (*local_8 == *(char *)(param_3 + local_c)) goto LAB__text__00429a80;
    }
  }
  for (; *local_8 != '\0'; local_8 = local_8 + 1) {
    iVar1 = FUN__text__00429820(*local_8);
    if (iVar1 == 0) {
      for (local_c = 0; *(char *)(param_2 + local_c) != '\0'; local_c = local_c + 1) {
        if (*local_8 == *(char *)(param_2 + local_c)) goto LAB__text__00429a80;
      }
    }
    else {
      local_8 = local_8 + 1;
    }
  }
LAB__text__00429a80:
  local_8 = (char *)0x429a8d;
  FUN__text__0056ce80();
  return;
}

