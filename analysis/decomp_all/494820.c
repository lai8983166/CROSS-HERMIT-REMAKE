
void __fastcall FUN__text__00494820(int param_1)

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
  if ((((*(char *)(param_1 + 0x108b3a) != '\0') && (*(short *)(param_1 + 0x108b32) != 0)) &&
      (*(char *)(param_1 + 0x108b34) != '\0')) &&
     (((*(char *)(param_1 + 0x108b36) != '\0' && (*(char *)(param_1 + 0x108b38) != '\0')) &&
      (local_8 = param_1, iVar1 = FUN__text__004577f0(), iVar1 == 0)))) {
    FUN__text__004128f0(0x1e,1);
  }
  local_8 = 0x4948e3;
  FUN__text__0056ce80();
  return;
}

