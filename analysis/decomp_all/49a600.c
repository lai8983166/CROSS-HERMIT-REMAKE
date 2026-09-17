
void __fastcall FUN__text__0049a600(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  char local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0x108b3e;
  if (((*(char *)(param_1 + 0x108b48) != '\0') && (*(char *)(param_1 + 0x108b3e) != '\0')) &&
     (*(char *)(param_1 + 0x108b4a) < '\x04')) {
    *(undefined2 *)(param_1 + 0xde708) = 0x40;
    local_8 = param_1;
    FUN__text__00407870(0x5a,10);
    *(undefined4 *)(local_8 + 0xde70c) = 0;
    *(undefined1 *)(local_8 + 0xde717) = 0xff;
    *(undefined1 *)(local_8 + 0xde716) = 0x80;
    *(undefined1 *)(local_8 + 0xde715) = 0x80;
    *(undefined1 *)(local_8 + 0xde714) = 0x80;
    *(undefined2 *)(local_8 + 0xde726) = 0xc6;
    local_14 = *(char *)(local_c + 9);
    if (local_14 == '\x01') {
      *(undefined2 *)(local_8 + 0xde728) = DAT_0061a050;
      *(undefined2 *)(local_8 + 0xde72a) = DAT_0061a052;
      *(undefined2 *)(local_8 + 0xde72c) = DAT_0061a054;
      *(undefined2 *)(local_8 + 0xde72e) = DAT_0061a056;
      *(short *)(local_8 + 0xde6e8) =
           (*(short *)(local_8 + 0xde72c) - *(short *)(local_8 + 0xde728)) + 1;
      *(short *)(local_8 + 0xde6ea) =
           (*(short *)(local_8 + 0xde72e) - *(short *)(local_8 + 0xde72a)) + 1;
      FUN__text__004079c0(0x1cf,0x2d8);
    }
    else if (local_14 == '\x02') {
      *(undefined2 *)(local_8 + 0xde728) = DAT_0061a058;
      *(undefined2 *)(local_8 + 0xde72a) = DAT_0061a05a;
      *(undefined2 *)(local_8 + 0xde72c) = DAT_0061a05c;
      *(undefined2 *)(local_8 + 0xde72e) = DAT_0061a05e;
      *(short *)(local_8 + 0xde6e8) =
           (*(short *)(local_8 + 0xde72c) - *(short *)(local_8 + 0xde728)) + 1;
      *(short *)(local_8 + 0xde6ea) =
           (*(short *)(local_8 + 0xde72e) - *(short *)(local_8 + 0xde72a)) + 1;
      FUN__text__004079c0(0x1cf,0x2d8);
    }
    *(undefined2 *)(local_8 + 0xde728) = DAT_0061a048;
    *(undefined2 *)(local_8 + 0xde72a) = DAT_0061a04a;
    *(undefined2 *)(local_8 + 0xde72c) = DAT_0061a04c;
    *(undefined2 *)(local_8 + 0xde72e) = DAT_0061a04e;
    *(short *)(local_8 + 0xde6e8) =
         (*(short *)(local_8 + 0xde72c) - *(short *)(local_8 + 0xde728)) + 1;
    *(short *)(local_8 + 0xde6ea) =
         (*(short *)(local_8 + 0xde72e) - *(short *)(local_8 + 0xde72a)) + 1;
    FUN__text__004079c0(0x1cc,0x2af);
    *(undefined2 *)(local_8 + 0xde708) = 0;
    FUN__text__00407870(0x5a,9);
    FUN__text__004079c0(0x1cc,0x260);
    FUN__text__0049a9b0(0x2f8,0x2af,(int)*(char *)(local_c + 8),0);
    FUN__text__0049a9b0(0x2f8,0x2c2,(int)*(char *)(local_c + 7),0);
    if ((*(int *)(local_8 + 0x108b50) < (int)*(char *)(local_c + 8)) ||
       ((int)*(char *)(local_c + 7) < *(int *)(local_8 + 0x108b50))) {
      local_10 = 4;
    }
    else {
      local_10 = 0;
    }
    FUN__text__0049a9b0(0x270,0x2ba,*(undefined4 *)(local_8 + 0x108b50),local_10);
  }
  local_8 = 0x49a9aa;
  FUN__text__0056ce80();
  return;
}

