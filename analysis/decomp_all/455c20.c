
void __fastcall FUN__text__00455c20(int param_1)

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
  _memset((void *)(*(int *)(param_1 + 0x60) + 0x2234),0,0x200);
  for (local_c = 0; local_c != 0x20; local_c = local_c + 1) {
    *(undefined1 *)(*(int *)(local_8 + 0x60) + 0x2234 + local_c * 0x10) = 0xff;
  }
  FUN__text__00455d00(0);
  local_8 = 0x455c9e;
  FUN__text__0056ce80();
  return;
}

