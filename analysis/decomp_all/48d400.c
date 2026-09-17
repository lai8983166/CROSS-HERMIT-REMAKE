
void __fastcall FUN__text__0048d400(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  void *local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (void *)(param_1 + 0x113a60);
  local_8 = param_1;
  _memset(local_c,0,0x204c);
  *(undefined1 *)((int)local_c + 0xc) = *(undefined1 *)(local_8 + 0x2ef44);
  *(undefined1 *)((int)local_c + 0xd) = 4;
  *(undefined4 *)((int)local_c + 0x18) = *(undefined4 *)(local_8 + 0x2e6f4);
  *(undefined4 *)((int)local_c + 0x28) = *(undefined4 *)(local_8 + 0x2e70c);
  *(undefined4 *)((int)local_c + 0x38) = *(undefined4 *)(local_8 + 0x2e710);
  local_8 = 0x48d48b;
  FUN__text__0056ce80();
  return;
}

