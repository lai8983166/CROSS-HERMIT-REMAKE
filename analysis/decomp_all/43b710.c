
void __fastcall FUN__text__0043b710(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [19];
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = *(int *)(DAT_007a49fc + 0x1970) + -0x1e;
  if ((iVar1 < 0) || (0x239 < iVar1)) {
    *(undefined2 *)(param_1 + 0x265b0) = 0xffff;
    *(undefined2 *)(param_1 + 0x265ae) = 0xffff;
  }
  else {
    *(short *)(param_1 + 0x265ae) =
         (short)*(undefined4 *)(DAT_007a49fc + 0x196c) + *(short *)(param_1 + 0x265a6);
    *(short *)(param_1 + 0x265b0) = (short)iVar1 + *(short *)(param_1 + 0x265a8);
  }
  return;
}

