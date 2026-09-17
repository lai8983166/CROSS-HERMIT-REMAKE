
void FUN__text__004e31c0(short param_1)

{
  short sVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  sVar1 = FUN__text__004d1ba0((int)param_1,0,0x7f);
  (&DAT_007d4f3c)[sVar1] = 0;
  local_8 = 0x4e3207;
  FUN__text__0056ce80();
  return;
}

