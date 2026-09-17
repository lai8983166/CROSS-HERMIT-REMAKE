
void FUN__text__00499560(undefined4 param_1,undefined4 param_2,uint param_3,uint param_4,
                        undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  switch(param_1) {
  case 0:
    FUN__text__004992d0(param_2);
    break;
  case 1:
    FUN__text__00499430(param_2,param_3,param_4,100);
    break;
  case 2:
    FUN__text__004993d0(param_2,param_3 & 0xffff,param_4 & 0xffff,param_5,100);
    break;
  case 3:
    FUN__text__00499480(param_2,param_3 & 0xffff,param_4 & 0xffff,param_5,100);
    break;
  case 4:
    FUN__text__004994e0(param_2);
    break;
  case 10:
    FUN__text__00497df0(param_2,param_3);
    goto LAB__text__0049973f;
  case 0x14:
    FUN__text__004972b0(param_2,param_3 & 0xffff);
    break;
  case 0x15:
    FUN__text__00497d10();
    break;
  case 0x16:
    FUN__text__00497f90(param_3);
    goto LAB__text__0049973f;
  case 0x17:
    FUN__text__00497ec0(param_3);
    goto LAB__text__0049973f;
  case 0x18:
    FUN__text__00498a40(0);
    break;
  case 0x19:
    FUN__text__00498f30(param_2,param_3);
    break;
  case 0x1a:
    FUN__text__004990a0(param_2,param_3,param_4 & 0xffff,param_5,param_6);
    goto LAB__text__0049973f;
  case 0x1b:
    FUN__text__00499520();
    break;
  case 0x1c:
    FUN__text__00498c40(param_2,param_3,param_4,param_5,param_6,param_7);
    break;
  case 0x1d:
    FUN__text__00498c90(param_2,param_3,param_4,param_5,param_6);
    break;
  case 0x1e:
    FUN__text__00498ce0(param_2);
    break;
  case 0x1f:
    FUN__text__00499200();
    break;
  case 0x20:
    FUN__text__00499240(param_2);
    break;
  case 0x21:
    FUN__text__00498e60(param_2);
    break;
  case 0x22:
    FUN__text__004976e0(param_2);
  }
  FUN__text__004977a0();
LAB__text__0049973f:
  local_8 = 0x49974c;
  FUN__text__0056ce80();
  return;
}

