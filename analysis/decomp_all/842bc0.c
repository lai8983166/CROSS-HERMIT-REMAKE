
void FUN__text1__00842bc0(int param_1,int param_2,int param_3)

{
  undefined2 uVar1;
  short sVar2;
  uint uVar3;
  int local_30;
  short asStack_28 [16];
  int local_8;
  
  sVar2 = 0;
  for (local_8 = 1; local_8 < 0x10; local_8 = local_8 + 1) {
    sVar2 = (sVar2 + *(short *)(param_3 + -2 + local_8 * 2)) * 2;
    asStack_28[local_8] = sVar2;
  }
  for (local_30 = 0; local_30 <= param_2; local_30 = local_30 + 1) {
    uVar3 = (uint)*(ushort *)(param_1 + 2 + local_30 * 4);
    if (uVar3 != 0) {
      sVar2 = asStack_28[uVar3];
      asStack_28[uVar3] = asStack_28[uVar3] + 1;
      uVar1 = FUN__text1__008448fc(sVar2,uVar3);
      *(undefined2 *)(param_1 + local_30 * 4) = uVar1;
    }
  }
  return;
}

