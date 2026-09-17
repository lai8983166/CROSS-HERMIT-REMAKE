
void __fastcall FUN__text__00430330(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined1 local_c;
  int local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (undefined1)((uint)*(undefined4 *)(param_1 + 0x34) >> 8);
  local_8 = param_1;
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0x94) = 0x80;
  *(undefined4 *)(local_8 + 0x98) = 1;
  *(undefined1 *)(local_8 + 0xa3) = local_c;
  *(undefined1 *)(local_8 + 0xa0) = 0x80;
  *(undefined1 *)(local_8 + 0xa1) = 0x80;
  *(undefined1 *)(local_8 + 0xa2) = 0x80;
  *(undefined2 *)(local_8 + 0xb2) = 100;
  FUN__text__00407870(0x5a,*(undefined4 *)(local_8 + 0x38));
  FUN__text__004079c0(0,0);
  local_8 = 0x4303f0;
  FUN__text__0056ce80();
  return;
}

