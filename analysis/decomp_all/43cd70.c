
void __fastcall FUN__text__0043cd70(int param_1)

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
  if ((*(int *)(param_1 + 0x265d8) != 0) && (*(int *)(param_1 + 0x265dc) == 1)) {
    local_8 = param_1;
    FUN__text__00410680(*(undefined4 *)(DAT_007a49fc + 0x19bc),
                        *(undefined4 *)(DAT_007a49fc + 0x19c0),
                        *(undefined4 *)(DAT_007a49fc + 0x196c),
                        *(undefined4 *)(DAT_007a49fc + 0x1970),2,0x80ffffff,2);
  }
  local_8 = 0x43cdff;
  FUN__text__0056ce80();
  return;
}

