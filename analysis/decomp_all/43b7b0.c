
void __fastcall FUN__text__0043b7b0(int param_1)

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
  local_8 = param_1;
  if ((((*(char *)(param_1 + 0x26596) == '\0') && (*(int *)(DAT_007a49fc + 0x19b8) == 0)) &&
      (iVar1 = FUN__text__0043c920(), iVar1 == 0)) &&
     ((((*(uint *)(DAT_007a49fc + 0x1990) & 2) != 0 && (*(short *)(local_8 + 0x265ae) != -1)) &&
      (*(short *)(local_8 + 0x265b0) != -1)))) {
    *(undefined4 *)(local_8 + 0x265e0) = 1;
    *(undefined2 *)(local_8 + 0x265e4) = *(undefined2 *)(local_8 + 0x265ae);
    *(undefined2 *)(local_8 + 0x265e6) = *(undefined2 *)(local_8 + 0x265b0);
  }
  else {
    *(undefined4 *)(local_8 + 0x265e0) = 0;
    *(undefined2 *)(local_8 + 0x265e4) = 0xffff;
    *(undefined2 *)(local_8 + 0x265e6) = 0xffff;
  }
  local_8 = 0x43b8ac;
  FUN__text__0056ce80();
  return;
}

