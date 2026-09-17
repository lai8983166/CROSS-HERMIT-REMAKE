
void FUN__text__00440e60(short *param_1,short *param_2)

{
  short sVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  short local_c;
  int local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_14 = (int)*param_1;
  local_c = __ftol();
  local_18 = (int)*param_2;
  sVar2 = __ftol();
  sVar1 = *(short *)(local_8 + 0x26470);
  *param_1 = local_c + *(short *)(local_8 + 0x2646c);
  *param_2 = sVar2 + sVar1;
  return;
}

