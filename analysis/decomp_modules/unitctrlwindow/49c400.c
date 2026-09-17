
void __fastcall FUN__text__0049c400(int param_1)

{
  uint uVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined2 local_10;
  undefined2 local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(undefined1 *)(param_1 + 0x2f160) = 0;
  if (((*(char *)(param_1 + 0x108b48) == '\0') && (*(char *)(param_1 + 0x108b3a) != '\0')) &&
     (*(int *)(DAT_007a49fc + 0x19b8) == 0)) {
    local_c = *(undefined2 *)(DAT_007a49fc + 0x196c);
    local_10 = *(undefined2 *)(DAT_007a49fc + 0x1970);
    uVar1 = (uint)DAT_007a49fc >> 0x10;
    *(undefined1 *)(param_1 + 0x2f15c) = 0xff;
    *(undefined1 *)(param_1 + 0x2f15e) = 0xff;
    local_8 = param_1;
    iVar2 = FUN__text__0049c560(local_c,CONCAT22((short)uVar1,local_10));
    if (iVar2 == 0) {
      FUN__text__0049c670(local_c,CONCAT22(extraout_var,local_10));
    }
    if ((*(char *)(local_8 + 0x2f15c) != -1) &&
       ((*(char *)(local_8 + 0x2f15c) != *(char *)(local_8 + 0x2f15d) ||
        (*(char *)(local_8 + 0x2f15e) != *(char *)(local_8 + 0x2f15f))))) {
      FUN__text__0049c9b0();
      *(undefined1 *)(local_8 + 0x2f15d) = *(undefined1 *)(local_8 + 0x2f15c);
      *(undefined1 *)(local_8 + 0x2f15f) = *(undefined1 *)(local_8 + 0x2f15e);
      *(undefined1 *)(local_8 + 0x2f160) = 1;
    }
  }
  local_8 = 0x49c551;
  FUN__text__0056ce80();
  return;
}

