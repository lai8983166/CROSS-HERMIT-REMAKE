
/* WARNING: Removing unreachable block (ram,0x0040e475) */
/* WARNING: Removing unreachable block (ram,0x0040e487) */
/* WARNING: Removing unreachable block (ram,0x0040e492) */
/* WARNING: Removing unreachable block (ram,0x0040e4a3) */
/* WARNING: Removing unreachable block (ram,0x0040e4b2) */
/* WARNING: Removing unreachable block (ram,0x0040e4bb) */
/* WARNING: Removing unreachable block (ram,0x0040e4c9) */
/* WARNING: Removing unreachable block (ram,0x0040e4cd) */
/* WARNING: Removing unreachable block (ram,0x0040e4e6) */
/* WARNING: Removing unreachable block (ram,0x0040e4f2) */
/* WARNING: Removing unreachable block (ram,0x0040e4e8) */
/* WARNING: Removing unreachable block (ram,0x0040e4a1) */
/* WARNING: Removing unreachable block (ram,0x0040e47e) */

void FUN__text__0040e330(void)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  uint local_10;
  int *local_c;
  int *local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__004144b0();
  if ((iVar2 != 1) &&
     (iVar2 = FUN__text__00424f80("DxSys->GetDrawEnable()==1",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                                  DAT_005ff358 + 5,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  iVar2 = FUN__text__004144b0();
  if (((iVar2 == 1) && (local_8[4] != 0)) && (*(int *)(*local_8 + 0xb284) == 0)) {
    FUN__text__00410310(0,0,1,1,0,0xff000000,0);
    local_8[6] = 1;
    local_10 = local_8[2];
    while (local_10 = local_10 - 1, -1 < (int)local_10) {
      if (*(int *)(local_8[4] + local_10 * 8) != 0) {
        local_c = *(int **)(local_8[4] + local_10 * 8);
        while( true ) {
          if (*(int *)(*local_8 + 0xb284) != 0) goto LAB__text__0040e4f6;
          FUN__text__0040e510(local_c,local_10 & 0xffff);
          if (*local_c == 0) break;
          local_c = (int *)*local_c;
        }
      }
    }
  }
LAB__text__0040e4f6:
  local_8 = (int *)0x40e503;
  FUN__text__0056ce80();
  return;
}

