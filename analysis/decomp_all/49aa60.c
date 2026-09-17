
void __fastcall FUN__text__0049aa60(int param_1)

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
  _memset((void *)(param_1 + 0xdb86c),0,0xaa0);
  *(undefined4 *)(local_8 + 0xdb868) = 0;
  for (local_c = 0; local_c != 0xfa; local_c = local_c + 1) {
    iVar1 = FUN__text__00468d10(local_8 + 0x80aec + local_c * 0x520);
    if (iVar1 != 0) {
      iVar1 = FUN__text__0046a4c0(local_8 + 0x80aec + local_c * 0x520);
      if (iVar1 != 0) {
        *(int *)(local_8 + 0x80d48 + local_c * 0x520) =
             local_8 + 0xdb86c + *(int *)(local_8 + 0xdb868) * 0x88;
        *(int *)(local_8 + 0xdb868) = *(int *)(local_8 + 0xdb868) + 1;
      }
    }
  }
  local_8 = 0x49ab54;
  FUN__text__0056ce80();
  return;
}

