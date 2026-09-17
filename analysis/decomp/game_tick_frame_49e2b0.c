
void game_tick_frame(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 auStack_154 [16];
  uint uStack_114;
  int *piStack_8;
  
  puVar2 = auStack_154;
  for (iVar1 = 0x54; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  piStack_8 = (int *)(DAT_007a4a00 + 0x2c);
  if (*piStack_8 == 1) {
    uStack_114 = *(uint *)(DAT_007a4a00 + 0x30);
    if (uStack_114 < 0x19) {
                    /* WARNING: Could not recover jumptable at 0x0049e304. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(&UNK_0049e4d3 + uStack_114 * 4))();
      return;
    }
    *piStack_8 = 0;
  }
  func_0x0049e540();
  piStack_8 = (int *)&UNK_0049e4cf;
  __chkesp();
  return;
}

