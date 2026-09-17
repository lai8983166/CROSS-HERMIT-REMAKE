
undefined1 __fastcall FUN__text__004c7ab0(short *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [17];
  undefined1 local_c;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 == 0) {
    local_c = 1;
  }
  else {
    switch(param_1[1]) {
    case 0:
    case 2:
    case 100:
      local_c = 1;
      break;
    case 3:
    case 4:
    case 5:
    case 6:
      local_c = 0;
    }
  }
  return local_c;
}

