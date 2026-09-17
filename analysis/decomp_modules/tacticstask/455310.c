
void __fastcall FUN__text__00455310(int param_1)

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
  local_8 = param_1;
  _memset((void *)(*(int *)(param_1 + 0x60) + 0x20ec),0,0x80);
  for (local_c = 0; local_c != 0x10; local_c = local_c + 1) {
    *(undefined1 *)(*(int *)(local_8 + 0x60) + 0x20ec + local_c * 8) = 0xff;
  }
  FUN__text__004553e0(0);
  local_8 = 0x45538b;
  FUN__text__0056ce80();
  return;
}

