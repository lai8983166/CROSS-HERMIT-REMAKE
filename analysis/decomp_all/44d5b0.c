
void __fastcall FUN__text__0044d5b0(int param_1)

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
  DAT_0080933c = *(undefined4 *)(param_1 + 0x48);
  DAT_00809340 = *(undefined4 *)(param_1 + 0x4c);
  DAT_00809344 = *(undefined4 *)(param_1 + 0x50);
  local_8 = param_1;
  FUN__text__004e2d00(&DAT_00809320);
  local_8 = 0x44d60a;
  FUN__text__0056ce80();
  return;
}

