
uint FUN__text__004c2060(int param_1,int param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  uint local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  switch(param_3) {
  case 1:
    local_c = (uint)(param_1 == param_2);
    break;
  case 2:
    local_c = (uint)(param_1 != param_2);
    break;
  case 3:
    local_c = (uint)(param_2 < param_1);
    break;
  case 4:
    local_c = (uint)(param_2 <= param_1);
    break;
  case 5:
    local_c = (uint)(param_1 < param_2);
    break;
  case 6:
    local_c = (uint)(param_1 <= param_2);
  }
  return local_c;
}

