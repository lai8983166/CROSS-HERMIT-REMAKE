
void __fastcall FUN__text__00494db0(int param_1)

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
  local_c = 0;
  do {
    if (local_c == 0x200) {
LAB__text__00494e54:
      local_8 = 0x494e61;
      FUN__text__0056ce80();
      return;
    }
    if ((*(byte *)(param_1 + 0x2c6f0 + local_c * 0x10) & 0x80) == 0) {
      local_8 = param_1;
      FUN__text__00494d70(param_1 + 0x2c6f0 + local_c * 0x10);
      *(byte *)(local_8 + 0x2c6f0 + local_c * 0x10) =
           *(byte *)(local_8 + 0x2c6f0 + local_c * 0x10) | 0x80;
      goto LAB__text__00494e54;
    }
    local_c = local_c + 1;
  } while( true );
}

