
void __thiscall FUN__text__0041d7f0(int *param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if ((((*param_1 != 0) && (param_1[1] != 0)) && (param_1[2] != 0)) &&
     ((param_1[5] != 0 && (local_8 = param_1, iVar1 = FUN__text__0041d790(), iVar1 != 0)))) {
    if (param_2 == 1) {
      iVar1 = FUN__text__0041d7c0();
      if (iVar1 != 0) {
        FUN__text__0041e620();
      }
    }
    else if (*(char *)((int)local_8 + 0x22) != '\0') {
      FUN__text__0041e590();
    }
  }
  local_8 = (int *)0x41d88e;
  FUN__text__0056ce80();
  return;
}

