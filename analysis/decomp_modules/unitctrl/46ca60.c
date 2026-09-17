
ushort __thiscall FUN__text__0046ca60(int param_1,int param_2)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [18];
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((*(char *)(*(int *)(param_2 + 600) + 0x9d) == '\0') ||
      (uVar1 = *(ushort *)
                (*(int *)(param_2 + 600) + 0x84 +
                (uint)*(byte *)(*(int *)(param_2 + 600) + 0x9e) * 2), (uVar1 & 0x8000) != 0)) ||
     (uVar1 == 0)) {
    uVar1 = *(ushort *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 0x80d44) + 0xc) * 0x40)
    ;
  }
  return uVar1;
}

