
void FUN__text__0046df90(int param_1,undefined4 param_2,undefined4 param_3,int param_4)

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
  iVar1 = FUN__text__00468d10(param_1);
  if ((iVar1 != 0) && (iVar1 = FUN__text__0046a430(param_1), iVar1 != 0)) {
    local_c = param_4;
    if (param_4 == 0) {
      *(undefined2 *)(local_8 + 0xde5a6) = 199;
      *(undefined1 *)(local_8 + 0xde597) = 0xff;
      *(undefined1 *)(local_8 + 0xde596) = 0x80;
      *(undefined1 *)(local_8 + 0xde595) = 0x80;
      *(undefined1 *)(local_8 + 0xde594) = 0x80;
      *(undefined4 *)(local_8 + 0xde58c) = 0;
      *(undefined2 *)(local_8 + 0xde588) = 0x88;
    }
    else if (param_4 == 1) {
      *(undefined2 *)(local_8 + 0xde5a6) = 199;
      *(undefined1 *)(local_8 + 0xde597) = 0xb8;
      *(undefined1 *)(local_8 + 0xde596) = 0x90;
      *(undefined1 *)(local_8 + 0xde595) = 0x90;
      *(undefined1 *)(local_8 + 0xde594) = 0x90;
      *(undefined4 *)(local_8 + 0xde58c) = 1;
      *(undefined2 *)(local_8 + 0xde588) = 0x88;
    }
    FUN__text__004077c0(DAT_007a49fc);
    FUN__text__00407870(0x5a,*(ushort *)(*(int *)(param_1 + 600) + 2) + 0x1e);
    FUN__text__004079c0(param_2,param_3);
  }
  local_8 = 0x46e0e5;
  FUN__text__0056ce80();
  return;
}

