
undefined4
FUN__text__00470070(short param_1,short param_2,short param_3,short param_4,short param_5,
                   short param_6)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [17];
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if ((((param_5 < param_1) || ((int)param_1 + (int)param_3 <= (int)param_5)) || (param_6 < param_2)
      ) || ((int)param_2 + (int)param_4 <= (int)param_6)) {
    uVar1 = 0;
  }
  else {
    uVar1 = 1;
  }
  return uVar1;
}

