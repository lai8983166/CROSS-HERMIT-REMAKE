
void __thiscall FUN__text__00467850(int param_1,undefined1 param_2,undefined1 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  int local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  if (*(char *)(param_1 + 0x108b3b) != -1) {
    FUN__text__0042b2d0(&DAT_0059c4ac);
  }
  *(undefined1 *)(local_8 + 0x108b3b) = param_2;
  *(undefined1 *)(local_8 + 0x108b3c) = param_3;
  local_8 = 0x4678ae;
  FUN__text__0056ce80();
  return;
}

