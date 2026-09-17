
void __fastcall FUN__text__00460520(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; local_8 = param_1, iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
LAB__text__0046053d:
  local_10 = *(undefined4 *)(local_8 + 0x30);
  switch(local_10) {
  case 0:
    FUN__text__004db060(0x20,0);
    FUN__text__00460810();
    *(undefined4 *)(local_8 + 0x30) = 1;
    break;
  case 1:
    local_14 = FUN__text__004606f0();
    local_c = local_14;
    switch(local_14) {
    case 0:
    case 1:
      *(undefined4 *)(local_8 + 0x30) = 0x14;
      break;
    case 2:
      *(undefined4 *)(local_8 + 0x30) = 10;
      break;
    case 3:
    case 4:
    case 5:
      *(undefined4 *)(local_8 + 0x30) = 0x14;
      break;
    case 6:
      *(undefined4 *)(local_8 + 0x30) = 0x14;
    }
    break;
  case 10:
    iVar1 = FUN__text__00460b10();
    if (iVar1 == 0) {
      *(undefined4 *)(local_8 + 0x30) = 0x14;
    }
    else {
      *(undefined4 *)(local_8 + 0x30) = 1;
    }
    break;
  case 0x14:
    FUN__text__00460a50();
    local_18 = local_c;
    switch(local_c) {
    case 0:
    case 1:
    case 2:
    case 6:
      FUN__text__004db120();
      local_8 = 0x460680;
      FUN__text__0056ce80();
      return;
    case 3:
    case 4:
    case 5:
      FUN__text__00460dd0(local_c);
      FUN__text__00460d50(local_c);
      FUN__text__00460e90(local_c);
      FUN__text__004609a0();
      *(undefined4 *)(local_8 + 0x30) = 1;
      break;
    default:
      goto switchD__text__00460568_caseD_2;
    }
    goto LAB__text__0046053d;
  }
switchD__text__00460568_caseD_2:
  goto LAB__text__0046053d;
}

