
void FUN__text__00453650(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  int local_c;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_c = 0; local_c != param_2; local_c = local_c + 1) {
    *(undefined *)(param_1 + 7 + local_c * 0x54) = (&DAT_0060c900)[local_c * 4];
    *(undefined *)(param_1 + 8 + local_c * 0x54) = (&DAT_0060c902)[local_c * 4];
  }
  return;
}

