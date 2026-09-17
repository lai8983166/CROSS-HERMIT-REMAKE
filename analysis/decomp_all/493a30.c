
void __fastcall FUN__text__00493a30(int param_1)

{
  undefined1 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != 5; local_c = local_c + 1) {
    if (*(char *)(local_8 + 0x116254 + local_c * 0x524) != '\0') {
      local_10 = local_8 + 0x116258 + local_c * 0x524;
      uVar1 = FUN__text__0040a100(local_10 + 0x48);
      *(undefined1 *)(local_10 + 4) = uVar1;
      if (*(char *)(local_10 + 4) != '\0') {
        if (*(char *)(local_8 + 0x116255 + local_c * 0x524) == '\0') {
          FUN__text__00409ff0(local_10 + 0x48,0,0x2d,0);
        }
        else {
          FUN__text__00409ff0(local_10 + 0x48,3,0x87,0);
        }
      }
      *(short *)(local_8 + 0x116256 + local_c * 0x524) =
           *(short *)(local_8 + 0x116256 + local_c * 0x524) + -1;
      if (*(short *)(local_8 + 0x116256 + local_c * 0x524) < 1) {
        *(undefined1 *)(local_8 + 0x116254 + local_c * 0x524) = 0;
      }
    }
  }
  local_8 = 0x493b75;
  FUN__text__0056ce80();
  return;
}

