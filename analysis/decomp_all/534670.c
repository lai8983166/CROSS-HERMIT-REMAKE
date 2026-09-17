
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN__text__00534670(int param_1,int param_2,int param_3,float *param_4)

{
  ushort *puVar1;
  float fVar2;
  ushort *puVar3;
  
  fVar2 = _DAT_005d0e78;
  puVar3 = (ushort *)
           (*(int *)(param_1 + 0x1050) * param_2 + *(int *)(param_1 + 0x1054) * param_3 +
           *(int *)(param_1 + 0x18));
  puVar1 = puVar3 + *(int *)(param_1 + 0x1058);
  for (; puVar3 < puVar1; puVar3 = puVar3 + 1) {
    *param_4 = (float)(*(byte *)((int)puVar3 + 1) & 0xf) * fVar2;
    param_4[1] = (float)(byte)((byte)*puVar3 >> 4) * fVar2;
    param_4[2] = (float)((byte)*puVar3 & 0xf) * fVar2;
    param_4[3] = (float)(*puVar3 >> 0xc) * fVar2;
    param_4 = param_4 + 4;
  }
  if (*(int *)(param_1 + 0x10) != 0) {
    FUN__text__005324ac(param_4 + *(int *)(param_1 + 0x1058) * -4);
  }
  return;
}

