
void FUN__text__004997d0(undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_4c;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1;
  switch(param_1) {
  case 0:
    FUN__text__00497560();
    break;
  case 1:
    FUN__text__00499160(param_2);
    break;
  case 2:
    FUN__text__00496fd0(param_2,param_3);
    break;
  case 3:
    FUN__text__00497040(param_2,param_3);
    break;
  case 4:
    FUN__text__00497630();
    break;
  case 5:
    FUN__text__00499280();
    break;
  case 6:
    FUN__text__00499010();
    break;
  case 7:
    FUN__text__00497500();
    break;
  case 8:
    FUN__text__004970a0();
  }
  local_8 = 0x499883;
  FUN__text__0056ce80();
  return;
}

